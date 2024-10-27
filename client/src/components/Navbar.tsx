import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { CheckCircleIcon, Cog6ToothIcon, HomeIcon, UserCircleIcon } from "@heroicons/react/24/outline";
import Logo from "assets/logo.svg";

interface NavbarProps {
  title: string; 
}

/**
 * Component for Project Navbar
 */
const Navbar: React.FC<NavbarProps> = ({ title }) => {
  const navigate = useNavigate();

  return (
    <div
      className={`fixed z-10 h-14 w-[calc(100%-16rem)] bg-white dark:bg-dark-bgColor`}
    >
      <>
        <div className="mx-auto w-full px-2 sm:px-6 lg:px-8">
          <div className="relative flex h-14 items-center justify-between">
            <div className="flex flex-1 items-center justify-center sm:items-stretch sm:justify-start">
              <div className="flex flex-shrink-0 items-center">
                <button
                  onClick={() => {
                    navigate(`/`);
                  }}
                  type="button"
                  className="text-base hover:text-tertiary"
                >
                  <HomeIcon className="h-5 w-5 dark:text-dark-textColor" />
                </button> 
                  <>
                    <span className="px-1.5 text-sm font-semibold dark:text-dark-textColor">
                      /
                    </span>
                    <p className="text-base font-semibold dark:text-dark-textColor">
                      {title}
                    </p>
                  </> 
              </div>
            </div>

            <div className="absolute inset-y-0 right-0 flex items-center space-x-2 pr-2 sm:static sm:inset-auto sm:ml-6 sm:pr-0">
              <div className="flex items-center space-x-1 rounded-lg border border-borderColor px-5 py-1 dark:border-dark-borderColor">
                  <UserCircleIcon className="h-4 w-4 dark:text-dark-textColor" />
                <p className="text-sm text-tertiary dark:text-dark-textColor">
                  Account
                </p>
              </div>
            </div>
          </div>
        </div>
      </>
    </div>
  );
};

export default Navbar;
