package com.meluhans.feeder33;


import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.ListView;
import android.widget.Toast;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.sql.Time;
import java.text.ParseException;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.Date;
import java.util.List;

import static android.content.Context.MODE_PRIVATE;


public class DeadlineFragment extends Fragment {

	ListView deadlineListView;
	List<DeadlineItem> deadlineList;
	DeadlineListAdapter adapter;
	String date;

	public DeadlineFragment() {
		// Required empty public constructor
	}


	@Override
	public View onCreateView(LayoutInflater inflater, ViewGroup container,
	                         Bundle savedInstanceState) {
		// Inflate the layout for this fragment
		View view = inflater.inflate(R.layout.fragment_deadline, container, false);

		deadlineListView = (ListView) view.findViewById(R.id.deadlineListView);
		deadlineList = new ArrayList<>();

		date = getArguments().getString("date", null);

		try {
			if (date == null)
				populateList();
			else
				populateList(date);
		} catch (JSONException e) {
			e.printStackTrace();
		} catch (ParseException e) {
			e.printStackTrace();
		}

		adapter = new DeadlineListAdapter(getActivity().getApplicationContext(), deadlineList, R.layout.item_deadline);
		deadlineListView.setAdapter(adapter);

		deadlineListView.setOnItemClickListener(new AdapterView.OnItemClickListener() {
			@Override
			public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
				DeadlineItem item = deadlineList.get(position);
				if (item.getIsFeedback()) {
					int feedbackId = item.getFeedbackId();
					SharedPreferences pref = getActivity().getSharedPreferences(LoginActivity.PREF_NAME, MODE_PRIVATE);
					if (pref.contains(Integer.toString(feedbackId) + "_" + pref.getString(LoginActivity.PREF_USER_KEY, null))) {
						toast("You have already filled this feedback :)");
					} else {
						Intent intent = new Intent(getActivity(), FeedbackActivity.class);
						intent.putExtra("id", feedbackId);
						startActivity(intent);
					}
				} else {
					Intent intent = new Intent(getActivity(), DetailActivity.class);
					intent.putExtra("course", item.getCourseCode());
					intent.putExtra("assignment", item.getAssignment());
					intent.putExtra("date", Utility.dateToString(item.getSubmissionDate()));
					intent.putExtra("time", Utility.timeToString(item.getSubmissionTime()));
					startActivity(intent);
				}
			}
		});

		return view;
	}

	/**
	 * populates deadlineList with all the deadlines available
	 * @throws JSONException
	 * @throws ParseException
	 */
	public void populateList() throws JSONException, ParseException {
		SharedPreferences pref = getActivity().getSharedPreferences(LoginActivity.PREF_NAME, MODE_PRIVATE);
		if (pref.contains(CalendarActivity.PREF_DEADLINE_KEY)) {
			String response = pref.getString(CalendarActivity.PREF_DEADLINE_KEY, null);

			JSONObject jsonObject = new JSONObject(response);
			JSONArray deadlines = jsonObject.getJSONArray("deadlines");

			Calendar today = Calendar.getInstance();

			for (int i = 0; i < deadlines.length(); ++i) {

				JSONObject d = deadlines.getJSONObject(i);
				String courseCode = d.getString("course");
				String assignment = d.getString("assignment");
				Boolean isFeedback = d.getBoolean("is_feedback");
				Date submissionDate = Utility.stringToDate(d.getString("submission_date"));
				Time submissionTime = Utility.stringToTime(d.getString("submission_time"));
				String id = d.getString("feedback_id");

				if (submissionDate.compareTo(today.getTime()) > 0
						|| Utility.dateToString(submissionDate).compareTo(Utility.dateToString(today.getTime())) == 0) {
					
					int feedbackId = -1;
					if (id.compareTo("null") != 0) {
						feedbackId = Integer.parseInt(id);
					}

					DeadlineItem item = new DeadlineItem(
							courseCode,
							assignment,
							isFeedback,
							submissionDate,
							submissionTime,
							feedbackId
					);
					deadlineList.add(item);
				}
			}

		}
	}

	/**
	 * populates deadlineList with deadlines with submission date as given parameter
	 * @param date
	 * @throws JSONException
	 * @throws ParseException
	 */
	public void populateList(String date) throws JSONException, ParseException {
		SharedPreferences pref = getActivity().getSharedPreferences(LoginActivity.PREF_NAME, MODE_PRIVATE);
		if (pref.contains(CalendarActivity.PREF_DEADLINE_KEY)) {
			String response = pref.getString(CalendarActivity.PREF_DEADLINE_KEY, null);
			JSONObject jsonObject = new JSONObject(response);
			JSONArray deadlines = jsonObject.getJSONArray("deadlines");

			for (int i = 0; i < deadlines.length(); ++i) {
				JSONObject d = deadlines.getJSONObject(i);
				if (date.equals(d.getString("submission_date"))) {
					String courseCode = d.getString("course");
					String assignment = d.getString("assignment");
					Boolean isFeedback = d.getBoolean("is_feedback");
					Date submissionDate = Utility.stringToDate(date);
					Time submissionTime = Utility.stringToTime(d.getString("submission_time"));
					String id = d.getString("feedback_id");

					int feedbackId = -1;
					if (id.compareTo("null") != 0) {
						feedbackId = Integer.parseInt(id);
					}

					DeadlineItem item = new DeadlineItem(
							courseCode,
							assignment,
							isFeedback,
							submissionDate,
							submissionTime,
							feedbackId
					);
					deadlineList.add(item);
				}
			}
		}
	}

	public void toast(String text) {
		Toast.makeText(getActivity(), text, Toast.LENGTH_SHORT).show();
	}
}
