package com.meluhans.feeder33;

import android.content.Intent;
import android.content.SharedPreferences;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.HashMap;
import java.util.Map;

public class LoginActivity extends AppCompatActivity {

	EditText rollno;
	EditText password;
	Button logInButton;

	public static final String PREF_NAME = "MyPref";
	public static final String PREF_USER_KEY = "user";
	public static final String PREF_ROLLNO_KEY = "rollno";
	public static final String PREF_AUTH_KEY = "authenticated";

	public static final String BASE_URL = "http://192.168.0.104:8033/student/";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);

	    checkIfAuthenticated();

	    rollno = (EditText) findViewById(R.id.rollno);
	    password = (EditText) findViewById(R.id.password);
	    logInButton = (Button) findViewById(R.id.logInButton);

	    logInButton.setOnClickListener(new View.OnClickListener() {
		    @Override
		    public void onClick(View v) {
			    String rollNumber = rollno.getText().toString();
			    String pass = password.getText().toString();
			    logIn(rollNumber, pass);
		    }
	    });
    }

	// checks if already someone is logged in or not
	// if logged in, redirects to dashboard
	public void checkIfAuthenticated() {
		SharedPreferences pref = getApplicationContext().getSharedPreferences(PREF_NAME, MODE_PRIVATE);
		Boolean authenticated = pref.getBoolean(PREF_AUTH_KEY, false);

		if (authenticated) {
			toast("Logged in as " + pref.getString(PREF_USER_KEY, ""));
			goToDashboard();
		}
	}

	// sends a POST request to Django server with rollNumber and password
	// server returns a JSON response, with three fields - "valid", "name", "error"
	// if valid is true, then credentials are valid and redirects to dashboard
	public void logIn(final String rollNumber, final String password) {

		String url = BASE_URL + "login/";
		RequestQueue queue = Volley.newRequestQueue(this);
		StringRequest postRequest = new StringRequest(Request.Method.POST, url,
				new Response.Listener<String>() {
					@Override
					public void onResponse(String response) {
						// response
						try {
							JSONObject jsonObject = new JSONObject(response);
							String valid = jsonObject.getString("valid");
							String name = jsonObject.getString("name");
							if (valid.compareTo("true") == 0) {
								toast("Welcome " + name);
								saveInPref(rollNumber, name);
								goToDashboard();
							} else {
								toast(jsonObject.getString("error"));
							}
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
				params.put("rollno", rollNumber);
				params.put("password", password);

				return params;
			}
		};
		queue.add(postRequest);

	}

	// redirects to DashboardActivity
	public void goToDashboard() {
		Intent intent = new Intent(this, DashboardActivity.class);
		startActivity(intent);
	}

	// saves credentials (rollNumber, name, authentication status) in SharedPreferences
	public void saveInPref(String rollNumber, String name) {
		SharedPreferences pref = getApplicationContext().getSharedPreferences(PREF_NAME, MODE_PRIVATE);
		SharedPreferences.Editor editor = pref.edit();

		editor.putString(PREF_USER_KEY, name);
		editor.putString(PREF_ROLLNO_KEY, rollNumber);
		editor.putBoolean(PREF_AUTH_KEY, true);
		editor.commit();
	}

	// creates a toast with given text
	public void toast(String text) {
		Toast.makeText(getApplicationContext(), text, Toast.LENGTH_SHORT).show();
	}
}
