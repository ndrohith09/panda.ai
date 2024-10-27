import React from "react";

interface MenuItemProps {
  icon: React.ReactNode;
  title: string;
  onClick: () => void;
  isActive: boolean;
}

/**
 * Util MenuItem component for sidebar
 */
export const MenuItem: React.FC<MenuItemProps> = ({
  icon,
  title,
  onClick,
  isActive,
}) => {
  return (
    <div
      className={`mt-2 flex cursor-pointer items-center rounded-lg py-1.5 pl-4 text-sm font-medium dark:text-dark-textColor text-secondary hover:rounded-lg ${isActive ? "border border-borderColor bg-bgColor dark:border-dark-secondary dark:bg-dark-bgColor" : "hover:bg-bgColor dark:hover:bg-dark-bgColor"}`}
      onClick={onClick}
    >
      <div className="pr-3">{icon}</div>
      <p>{title}</p>
    </div>
  );
};
 