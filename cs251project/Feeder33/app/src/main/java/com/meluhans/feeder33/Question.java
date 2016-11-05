package com.meluhans.feeder33;


public class Question {
	String question;
	String[] options;
	int answer;
	int id;

	public Question() {
		answer = -1;
	}

	public Question(String question, String[] options, int id) {
		this.question = question;
		this.options = options;
		this.id = id;
		answer = -1;
	}
}