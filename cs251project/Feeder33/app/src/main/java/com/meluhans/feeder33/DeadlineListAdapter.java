package com.meluhans.feeder33;


import android.content.Context;
import android.support.annotation.NonNull;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.TextView;

import java.util.List;

public class DeadlineListAdapter extends ArrayAdapter<DeadlineItem> {

	private Context context;
	private List<DeadlineItem> items;
	private static LayoutInflater inflater = null;
	int resourceId;

	public DeadlineListAdapter(Context context, List<DeadlineItem> items, int resource) {
		super(context, resource, items);
		this.context = context;
		this.items = items;
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

		DeadlineItemHolder holder = new DeadlineItemHolder();
		holder.item = items.get(position);
		holder.title = (TextView) row.findViewById(R.id.titleText);
		holder.detail = (TextView) row.findViewById(R.id.detailText);

		holder.title.setText(holder.item.getAssignment() + " - " + holder.item.getCourseCode());

		if (items.get(position).getIsFeedback()) {
			holder.detail.setText(String.format("Feedback | Submission Time : %s", Utility.timeToString(holder.item.getSubmissionTime())));
		} else {
			holder.detail.setText(String.format("Submission Time : %s", Utility.timeToString(holder.item.getSubmissionTime())));
		}

		row.setTag(holder);

		return row;
	}


	public static class DeadlineItemHolder {
		DeadlineItem item;
		TextView title;
		TextView detail;
	}
}
