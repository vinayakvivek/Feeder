package com.meluhans.feeder33;

import android.content.Intent;
import android.content.SharedPreferences;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.ListView;
import android.widget.TextView;
import android.widget.Toast;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.HashMap;
import java.util.Map;

public class FeedbackActivity extends AppCompatActivity {

	Feedback feedback;
	ListView questionListView;
	QuestionListAdapter adapter;
	TextView title;
	TextView course;
	Button submitButton;
	int feedbackId;

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);

		Intent intent = getIntent();
		feedbackId = intent.getIntExtra("id", 0);

		getFeedbackDetails(feedbackId);
	}

	public void onRadioButtonClicked(View view) {
		Question question = (Question) view.getTag();
		int position = feedback.questions.indexOf(question);
		feedback.questions.get(position).answer = getOption(view.getId());
	}

	public int getOption(int id) {
		switch (id) {
			case R.id.option1:
				return 1;
			case R.id.option2:
				return 2;
			case R.id.option3:
				return 3;
			case R.id.option4:
				return 4;
			case R.id.option5:
				return 5;
		}
		return -1;
	}

	public void initialise() {

		setContentView(R.layout.activity_feedback);

		title = (TextView) findViewById(R.id.feedbackTitle);
		title.setText(feedback.title);

		course = (TextView) findViewById(R.id.courseText);
		course.setText(feedback.course);

		submitButton = (Button) findViewById(R.id.submitButton);
		submitButton.setOnClickListener(new View.OnClickListener() {
			@Override
			public void onClick(View v) {

				boolean markedAll = true;
				for (Question q : feedback.questions) {
					if (q.answer == -1) {
						markedAll = false;
						break;
					}
				}

				if (markedAll) {
					String url = LoginActivity.BASE_URL + "feedback/submit/";
					RequestQueue queue = Volley.newRequestQueue(getApplicationContext());
					for (final Question q : feedback.questions) {
						StringRequest postRequest = new StringRequest(Request.Method.POST, url,
								new Response.Listener<String>() {
									@Override
									public void onResponse(String response) {
										// response
										Log.d("Response", response);
									}
								},
								new Response.ErrorListener() {
									@Override
									public void onErrorResponse(VolleyError error) {
										// error
										toast("Can't connect to server");
										Log.d("Error.Response", error.toString());
									}
								}
						) {
							@Override
							protected Map<String, String> getParams() {
								Map<String, String> params = new HashMap<String, String>();
								params.put("id", Integer.toString(q.id));
								params.put("option", Integer.toString(q.answer));
								return params;
							}
						};
						queue.add(postRequest);
					}

					saveInPrefs(feedback.id);

					Intent intent = new Intent(getApplicationContext(), CalendarActivity.class);
					startActivity(intent);
				} else {
					toast("Please mark a response for all questions");
				}
			}
		});

		questionListView = (ListView) findViewById(R.id.questionListView);
		adapter = new QuestionListAdapter(
				this,
				R.layout.item_question,
				feedback.questions
		);
		questionListView.setAdapter(adapter);
	}

	public void getFeedbackDetails(final int id) {

		String url = LoginActivity.BASE_URL + "feedback/";
		RequestQueue queue = Volley.newRequestQueue(this);
		StringRequest postRequest = new StringRequest(Request.Method.POST, url,
				new Response.Listener<String>() {
					@Override
					public void onResponse(String response) {
						// response
						try {
							JSONObject jsonObject = new JSONObject(response);
							String title = jsonObject.getString("title");
							String description = jsonObject.getString("description");
							String course = jsonObject.getString("course");

							feedback = new Feedback(title, description, course, feedbackId);

							JSONArray questions = jsonObject.getJSONArray("questions");
							for (int i = 0; i < questions.length(); ++i) {
								JSONObject q = questions.getJSONObject(i);
								String question = q.getString("question");
								int qId = q.getInt("question_id");
								String[] options = new String[5];
								options[0] = q.getString("a");
								options[1] = q.getString("b");
								options[2] = q.getString("c");
								options[3] = q.getString("d");
								options[4] = q.getString("e");
								feedback.addQuestion(question, qId, options);
							}

							initialise();

						} catch (JSONException e) {
							e.printStackTrace();
						}
						Log.d("Response", response);
					}
				},
				new Response.ErrorListener() {
					@Override
					public void onErrorResponse(VolleyError error) {
						// error
						toast("Can't connect to server");
						Log.d("Error.Response", error.toString());
					}
				}
		) {
			@Override
			protected Map<String, String> getParams() {
				Map<String, String>  params = new HashMap<String, String>();
				params.put("id", Integer.toString(id));
				return params;
			}
		};
		queue.add(postRequest);

	}

	public void toast(String text) {
		Toast.makeText(getApplicationContext(), text, Toast.LENGTH_LONG).show();
	}

	public void saveInPrefs(int feedbackId) {
		SharedPreferences pref = getApplicationContext().getSharedPreferences(LoginActivity.PREF_NAME, MODE_PRIVATE);
		SharedPreferences.Editor editor = pref.edit();
		// saved as "<feedback_id>_<username>"
		editor.putBoolean(Integer.toString(feedbackId) + "_" + pref.getString(LoginActivity.PREF_USER_KEY, null), true);
		editor.commit();
	}
}