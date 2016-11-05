package com.meluhans.feeder33;

import java.util.ArrayList;
import java.util.List;

public class Feedback {

	String title;
	String description;
	String course;
	int id;
	List<Question> questions;

	public Feedback(String title, String description, String course, int id) {
		this.title = title;
		this.description = description;
		this.course = course;
		this.id = id;
		questions = new ArrayList<Question>();
	}

	public void addQuestion(String q, int id, String[] options) {
		Question Q = new Question(q, options, id);
		questions.add(Q);
	}
}
