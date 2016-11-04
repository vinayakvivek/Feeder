package com.meluhans.feeder33;

import java.sql.Time;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Date;

public class Utility {

	public static String dateToString(Date date) {
		SimpleDateFormat ft = new SimpleDateFormat ("yyyy-MM-dd");
		return ft.format(date);
	}

	public static Date stringToDate(String dateString) throws ParseException {
		SimpleDateFormat ft = new SimpleDateFormat ("yyyy-MM-dd");
		return ft.parse(dateString);
	}

	public static String timeToString(Time time) {
		SimpleDateFormat ft = new SimpleDateFormat ("HH:mm");
		return ft.format(time);
	}

	public static Time stringToTime(String timeString) throws ParseException {
		SimpleDateFormat ft = new SimpleDateFormat ("HH:mm");
		return (Time) ft.parse(timeString);
	}
}
