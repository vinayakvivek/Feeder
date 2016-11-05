package com.meluhans.feeder33;


import java.sql.Time;
import java.util.Date;

public class DeadlineItem {

	private String courseCode;
	private String assignment;
	private Boolean isFeedback;
	private Date submissionDate;
	private Time submissionTime;
	private int feedbackId;

	public DeadlineItem(
			String courseCode,
			String assignment,
			Boolean isFeedback,
			Date submissionDate,
			Time submissionTime,
			int feedbackId
	) {
		this.courseCode = courseCode;
		this.assignment = assignment;
		this.isFeedback = isFeedback;
		this.submissionDate = submissionDate;
		this.submissionTime = submissionTime;
		if (isFeedback) {
			this.feedbackId = feedbackId;
		} else {
			this.feedbackId = -1;
		}
	}

	String getCourseCode() {return courseCode;}
	String getAssignment() {return assignment;}
	Boolean getIsFeedback() {return isFeedback;}
	Date getSubmissionDate() {return submissionDate;}
	Time getSubmissionTime() {return submissionTime;}
	int getFeedbackId() {return feedbackId;}
}
