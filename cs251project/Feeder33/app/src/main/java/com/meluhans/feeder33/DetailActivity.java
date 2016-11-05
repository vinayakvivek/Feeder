package com.meluhans.feeder33;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.TextView;

public class DetailActivity extends AppCompatActivity {

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_detail);

		Intent intent = getIntent();
		String course = intent.getStringExtra("course");
		String assignment = intent.getStringExtra("assignment");
		String date = intent.getStringExtra("date");
		String time = intent.getStringExtra("time");

		setTitle(course);

		TextView courseName = (TextView) findViewById(R.id.courseText);
		TextView title = (TextView) findViewById(R.id.titleText);
		TextView dateLabel = (TextView) findViewById(R.id.dateLabel);
		TextView dateText = (TextView) findViewById(R.id.date);
		TextView timeLabel = (TextView) findViewById(R.id.timeLabel);
		TextView timeText = (TextView) findViewById(R.id.time);

		courseName.setText(course);
		title.setText(assignment);
		dateLabel.setText("Submission Date");
		dateText.setText(date);

		timeLabel.setText("Submission Time");
		timeText.setText(time);
	}
}
