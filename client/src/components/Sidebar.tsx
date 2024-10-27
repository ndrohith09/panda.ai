import { useLocation, useNavigate } from "react-router-dom";
import { MenuItem } from "./Sidebar.utils";
import {
  HomeIcon,
  Cog6ToothIcon,
  CreditCardIcon,
} from "@heroicons/react/24/outline";
import Logo from "assets/logo-full.png";

const Sidebar = () => {
  const navigate = useNavigate();
  const location = useLocation();

  const pageRedirect = (path: string): void => {
    if (path) {
      navigate(`/${path}/`);
    } else {
      navigate(`/`);
    }
  };

  const IsStringInPath = (desiredStr: string) => {
    return location.pathname.includes(desiredStr);
  };


  return (
    <aside className="fixed left-0 top-0 flex h-screen w-64 flex-col border-r border-borderColor  dark:border-dark-sideBarBgColor dark:bg-dark-sideBarBgColor bg-gray-50 px-2 py-5">
      {/* Scrollable menu items */}
      <div className="flex-grow overflow-y-auto">
        <div className="flex-shrink-0 flex-col items-center">
          <img
            className="my-3 ml-6 h-10 dark:hidden block w-auto cursor-pointer"
            onClick={() => {
              pageRedirect("");
            }}
            src={Logo}
            alt="ZeroAgent"
          />
          <div className="mt-5 flex flex-col space-y-3 pl-2">
            <div className="text-secondary">
              <div className="flex flex-col space-y-2">
                <MenuItem
                  title={"Dashboard"}
                  onClick={() => {
                    pageRedirect("");
                  }}
                  isActive={IsStringInPath('')}
                  icon={
                    <HomeIcon
                      className={
                        "text-tertiary dark:text-dark-textColor w-4 h-4"
                      }
                    />
                  }
                />

                <MenuItem
                  title={"Pipeline"}
                  onClick={() => {
                    pageRedirect("pipeline");
                  }}
                  isActive={IsStringInPath('pipeline')}
                  icon={
                    <HomeIcon
                      className={
                        "text-tertiary dark:text-dark-textColor w-4 h-4"
                      }
                    />
                  }
                />

                <MenuItem
                  title={"Billing"}
                  onClick={() => {
                    navigate("billing");
                  }}
                  isActive={false}
                  icon={
                    <CreditCardIcon
                      className={
                        "text-tertiary dark:text-dark-textColor w-4 h-4"
                      }
                    />
                  }
                />
                <MenuItem
                  title={"Settings"}
                  onClick={() => {
                    navigate("settings");
                  }}
                  isActive={false}
                  icon={
                    <Cog6ToothIcon
                      className={
                        "text-tertiary dark:text-dark-textColor w-4 h-4"
                      }
                    />
                  }
                />
              </div>
            </div>
          </div>
        </div>
      </div>
    </aside>
  );
};

export default Sidebar;
