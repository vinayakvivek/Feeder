package com.meluhans.feeder33;

import android.content.Intent;
import android.content.SharedPreferences;
import android.graphics.Color;
import android.graphics.drawable.ColorDrawable;
import android.graphics.drawable.Drawable;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.Menu;
import android.view.MenuInflater;
import android.view.MenuItem;
import android.view.View;
import android.widget.Toast;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;
import com.roomorama.caldroid.CaldroidFragment;
import com.roomorama.caldroid.CaldroidListener;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.text.ParseException;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.Date;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class CalendarActivity extends AppCompatActivity {

	List<Drawable> colors = new ArrayList<>();
	List<String> courses = new ArrayList<>();
	Map<Date, Drawable> dateColorMap = new HashMap<>();
	Map<String, Drawable> courseColorMap = new HashMap<>();

	int noOfColors;

	CaldroidFragment caldroidFragment;
	CaldroidListener listener;

	public static final String PREF_DEADLINE_KEY = "deadlines";

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_calendar);

		colors.add(new ColorDrawable(Color.BLUE));
		colors.add(new ColorDrawable(Color.parseColor("#FF00FF")));
		colors.add(new ColorDrawable(Color.RED));
		colors.add(new ColorDrawable(Color.CYAN));
		colors.add(new ColorDrawable(Color.MAGENTA));

		noOfColors = colors.size();

		initialise();
	}

	@Override
	public boolean onCreateOptionsMenu(Menu menu) {
		MenuInflater inflater = getMenuInflater();
		inflater.inflate(R.menu.menu_calendar, menu);
		return true;
	}

	@Override
	public boolean onOptionsItemSelected(MenuItem item) {
		switch (item.getItemId()) {
			case R.id.logOutOption:
				Log.i("AppInfo", "clicked logOut");
				logOut();
				return true;
			default:
				return super.onOptionsItemSelected(item);
		}
	}

	public void logOut() {
		SharedPreferences pref = getApplicationContext().getSharedPreferences(LoginActivity.PREF_NAME, MODE_PRIVATE);
		SharedPreferences.Editor editor = pref.edit();

		editor.putString(LoginActivity.PREF_USER_KEY, "");
		editor.putString(LoginActivity.PREF_ROLLNO_KEY, "");
		editor.putBoolean(LoginActivity.PREF_AUTH_KEY, false);
		editor.commit();

		Intent intent = new Intent(this, LoginActivity.class);
		startActivity(intent);
	}

	/**
	 * Tries to fetch data from server
	 * if server is offline, looks for offline data
	 * parses the data obtained and then calendar is initialised
	 */
	public void initialise() {
		String url = LoginActivity.BASE_URL + "deadlines/";
		RequestQueue queue = Volley.newRequestQueue(this);
		StringRequest postRequest = new StringRequest(Request.Method.POST, url,
				new Response.Listener<String>() {
					@Override
					public void onResponse(String response) {
						// response
						try {
							JSONObject jsonObject = new JSONObject(response);
							saveDeadlines(jsonObject);
							parseData(jsonObject);
							initialiseCalendar();
						} catch (JSONException e) {
							e.printStackTrace();
						} catch (ParseException e) {
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

						SharedPreferences pref = getApplicationContext().getSharedPreferences(LoginActivity.PREF_NAME, MODE_PRIVATE);
						if (pref.contains(PREF_DEADLINE_KEY)) {
							toast("Showing offline data");
							try {
								parseData(new JSONObject(pref.getString(PREF_DEADLINE_KEY, null)));
								initialiseCalendar();
							} catch (JSONException e) {
								e.printStackTrace();
							} catch (ParseException e) {
								e.printStackTrace();
							}
						} else {
							toast("No offline data :(");
						}
					}
				}
		) {
			@Override
			protected Map<String, String> getParams() {
				Map<String, String>  params = new HashMap<String, String>();
				return params;
			}
		};
		queue.add(postRequest);
	}

	/**
	 * Initialises Caldroid fragment and Deadline fragment
	 */
	public void initialiseCalendar() {
		listener = new CaldroidListener() {
			@Override
			public void onSelectDate(Date date, View view) {
				toast(Utility.dateToString(date));
				DeadlineFragment deadlineFragment = new DeadlineFragment();
				Bundle args = new Bundle();
				args.putString("date", Utility.dateToString(date));
				deadlineFragment.setArguments(args);
				getSupportFragmentManager().beginTransaction()
						.replace(R.id.list_container, deadlineFragment)
						.commit();
			}
		};
		caldroidFragment = new CaldroidFragment();
		caldroidFragment.setBackgroundDrawableForDates(dateColorMap);
		Bundle args = new Bundle();
		Calendar cal = Calendar.getInstance();
		args.putInt(CaldroidFragment.THEME_RESOURCE, com.caldroid.R.style.CaldroidDefaultDark);
		args.putInt(CaldroidFragment.MONTH, cal.get(Calendar.MONTH) + 1);
		args.putInt(CaldroidFragment.YEAR, cal.get(Calendar.YEAR));
		caldroidFragment.setArguments(args);
		caldroidFragment.setCaldroidListener(listener);

		DeadlineFragment deadlineFragment = new DeadlineFragment();
		args = new Bundle();
		deadlineFragment.setArguments(args);

		getSupportFragmentManager().beginTransaction()
				.add(R.id.calender_container, caldroidFragment)
				.add(R.id.list_container, deadlineFragment)
				.commit();
	}

	/**
	 * Parses JSON data and populates courses, courseColorMap and dateColorMap
	 * @param jsonObject
	 * @throws JSONException
	 * @throws ParseException
	 */
	public void parseData(JSONObject jsonObject) throws JSONException, ParseException {
		JSONArray deadlines = jsonObject.getJSONArray("deadlines");

		for (int i = 0; i < deadlines.length(); ++i) {
			JSONObject d = deadlines.getJSONObject(i);
			String course = d.getString("course");
			if (!courses.contains(course)) {
				courses.add(course);
			}
		}

		for (int i = 0; i < courses.size(); ++i) {
			courseColorMap.put(courses.get(i), colors.get(i % noOfColors));
		}

		for (int i = 0; i < deadlines.length(); ++i) {
			JSONObject d = deadlines.getJSONObject(i);
			String course = d.getString("course");
			Date submissionDate = Utility.stringToDate(d.getString("submission_date"));
			dateColorMap.put(submissionDate, courseColorMap.get(course));
		}
	}

	/**
	 * Saves passes data as a String in Shared Preferences
	 * @param jsonObject
	 */
	public void saveDeadlines(JSONObject jsonObject) {
		SharedPreferences pref = getApplicationContext().getSharedPreferences(LoginActivity.PREF_NAME, MODE_PRIVATE);
		SharedPreferences.Editor editor = pref.edit();
		editor.putString(PREF_DEADLINE_KEY, jsonObject.toString());
		editor.commit();
	}

	public void toast(String text) {
		Toast.makeText(getApplicationContext(), text, Toast.LENGTH_SHORT).show();
	}
}
