package com.meluhans.feeder33;


import android.content.Context;
import android.support.annotation.NonNull;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.RadioButton;
import android.widget.TextView;

import java.util.List;

public class QuestionListAdapter extends ArrayAdapter<Question> {

	private Context context;
	private List<Question> items;
	private static LayoutInflater inflater = null;
	int resourceId;

	public QuestionListAdapter(Context context, int resource, List<Question> objects) {
		super(context, resource, objects);
		this.context = context;
		items = objects;
		inflater = (LayoutInflater) context.getSystemService(Context.LAYOUT_INFLATER_SERVICE);
		resourceId = resource;
	}

	@NonNull
	@Override
	public View getView(int position, View convertView, ViewGroup parent) {

		View row = convertView;
		if (row == null) {
			row = inflater.inflate(resourceId, parent, false);
		}

		QuestionHolder holder = new QuestionHolder();
		holder.item = items.get(position);
		holder.question = (TextView) row.findViewById(R.id.questionText);
		holder.options = new RadioButton[]{
				(RadioButton) row.findViewById(R.id.option1),
				(RadioButton) row.findViewById(R.id.option2),
				(RadioButton) row.findViewById(R.id.option3),
				(RadioButton) row.findViewById(R.id.option4),
				(RadioButton) row.findViewById(R.id.option5),
		};

		holder.question.setText(holder.item.question);
		for (int i = 0; i < 5; ++i) {
			holder.options[i].setText(holder.item.options[i]);
			holder.options[i].setTag(holder.item);
		}
		row.setTag(holder);
		return  row;
	}


	public static class QuestionHolder {
		Question item;
		TextView question;
		RadioButton[] options;
	}
}