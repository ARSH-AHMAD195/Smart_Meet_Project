// components/ActionItemList.jsx
import { formatDate } from "../../utils/utils";

function ActionItemList({ items }) {
  if (!items || items.length === 0) {
    return (
      <p className="px-10 text-gray-500">No action items available</p>
    );
  }

  return (
    <div className="w-full mt-5">
      {items.map(item => (
        <div
          key={item.id}
          className="px-10 flex justify-start py-2 text-black"
        >
          <span>{item.id}.</span>

          <div className="px-2 text-md font-medium">
            <span className="px-2">{item.task}</span>

            <span className="ml-3 px-2 bg-gray-100 outline-2 outline-gray-500 rounded-md">
              {item.assignee_name}
            </span>

            <span className="ml-3 px-2 bg-yellow-100 outline-2 outline-yellow-500 rounded-md">
              {formatDate(item.due_date)}
            </span>
          </div>
        </div>
      ))}
    </div>
  );
}

export default ActionItemList;
