package com.meluhans.feeder33;

import android.content.Intent;
import android.content.SharedPreferences;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;

public class DashboardActivity extends AppCompatActivity {

	private static String name;
	private static String rollNumber;

	Button logOutButton;

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_dashboard);

		getName();
		setTitle(name + "'s Dashboard");

		logOutButton = (Button) findViewById(R.id.logOutButton);
		logOutButton.setOnClickListener(new View.OnClickListener() {
			@Override
			public void onClick(View v) {
				logOut();
			}
		});
	}

	public void getName() {
		SharedPreferences pref = getApplicationContext().getSharedPreferences(LoginActivity.PREF_NAME, MODE_PRIVATE);
		name = pref.getString(LoginActivity.PREF_USER_KEY, "Anonymous");
		rollNumber = pref.getString(LoginActivity.PREF_ROLLNO_KEY, "Anonymous");
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
}
