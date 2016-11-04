package com.meluhans.feeder33;


import android.content.SharedPreferences;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ListView;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.sql.Time;
import java.text.ParseException;
import java.util.ArrayList;
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
		deadlineList = new ArrayList<DeadlineItem>();

		date = getArguments().getString("date", null);

		try {
			if (date == null)
				populateList();
			else
				updateList(date);
		} catch (JSONException e) {
			e.printStackTrace();
		} catch (ParseException e) {
			e.printStackTrace();
		}

		adapter = new DeadlineListAdapter(getActivity().getApplicationContext(), deadlineList, R.layout.item_deadline);
		deadlineListView.setAdapter(adapter);

		return view;
	}

	public void populateList() throws JSONException, ParseException {
		SharedPreferences pref = getActivity().getSharedPreferences(LoginActivity.PREF_NAME, MODE_PRIVATE);
		if (pref.contains(CalendarActivity.PREF_DEADLINE_KEY)) {
			String response = pref.getString(CalendarActivity.PREF_DEADLINE_KEY, null);

			JSONObject jsonObject = new JSONObject(response);
			JSONArray deadlines = jsonObject.getJSONArray("deadlines");

			for (int i = 0; i < deadlines.length(); ++i) {

				JSONObject d = deadlines.getJSONObject(i);
				String courseCode = d.getString("course");
				String assignment = d.getString("assignment");
				Boolean isFeedback = d.getBoolean("is_feedback");
				Date submissionDate = Utility.stringToDate(d.getString("submission_date"));
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

	public void updateList(String date) throws JSONException, ParseException {

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
}
