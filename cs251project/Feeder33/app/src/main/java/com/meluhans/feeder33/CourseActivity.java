package com.meluhans.feeder33;

import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.widget.ArrayAdapter;
import android.widget.ListView;
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

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;


public class CourseActivity extends AppCompatActivity {

	String rollno;
	ListView courseListView;
	List<String> courseList;
	ArrayAdapter<String> adapter;

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_course);

		setTitle("Enrolled courses");
		getRollNo();

		courseListView = (ListView) findViewById(R.id.courseListView);
		courseList = new ArrayList<>();

		populateList();
	}

	public void populateList() {
		String url = LoginActivity.BASE_URL + "courses/";
		RequestQueue queue = Volley.newRequestQueue(this);
		StringRequest postRequest = new StringRequest(Request.Method.POST, url,
				new Response.Listener<String>() {
					@Override
					public void onResponse(String response) {
						// response
						try {
							JSONObject jsonObject = new JSONObject(response);
							parseData(jsonObject);
							initialise();
						} catch (JSONException e) {
							e.printStackTrace();
						}
						Log.d("Response | deadlines ", response);
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
				params.put("rollno", rollno);
				return params;
			}
		};
		queue.add(postRequest);
	}

	public void initialise() {
		adapter = new ArrayAdapter<String>(this, android.R.layout.simple_expandable_list_item_1, courseList);
		courseListView.setAdapter(adapter);
	}

	public void parseData(JSONObject jsonObject) throws JSONException {
		JSONArray courses = jsonObject.getJSONArray("courses");
		for (int i = 0; i < courses.length(); ++i) {
			JSONObject course = courses.getJSONObject(i);
			courseList.add(course.getString("code") + " - " + course.getString("name"));
		}
	}

	public void getRollNo() {
		SharedPreferences pref = getApplicationContext().getSharedPreferences(LoginActivity.PREF_NAME, MODE_PRIVATE);
		if (pref.contains(LoginActivity.PREF_ROLLNO_KEY)) {
			rollno = pref.getString(LoginActivity.PREF_ROLLNO_KEY, null);
		} else {
			toast("Roll number does not exists");
			Intent intent = new Intent(this, CalendarActivity.class);
			startActivity(intent);
		}
	}

	public void toast(String text) {
		Toast.makeText(getApplicationContext(), text, Toast.LENGTH_SHORT).show();
	}

}
