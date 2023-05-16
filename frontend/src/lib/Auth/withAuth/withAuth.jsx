import React, { useEffect } from "react";
import { useDispatch } from "react-redux";
import { setAuth, setUser } from "../../Actions/auth";
import axiosInstance from "../../Axios/axiosInstance";
import Cookies from "js-cookie";

const withAuth = (WrappedComponent) => {
  const HOC = (props) => {
    const dispatch = useDispatch();

    useEffect(() => {
      if (Cookies.get("jwt")) {
        axiosInstance
          .get("auth/verify/")
          .then((res) => {
            console.log("token check:", res.data);
            dispatch(
              setAuth({
                is_authenticated: res.data.authenticated,
              })
            );
            dispatch(
              setUser({
                is_superuser: res.data.is_superuser,
                username: res.data.username,
              })
            );

            if (res.data.refreshed_token) {
              Cookies.remove("jwt");
              const expires = new Date(Date.parse(res.data.exp));
              Cookies.set("jwt", res.data.refreshed_token, { expires });
            }
          })
          .catch((err) => {
            dispatch(setAuth({ is_authenticated: false }));
            dispatch(
              setUser({
                is_superuser: false,
                username: "",
              })
            );
          });
      } else {
        dispatch(setAuth({ is_authenticated: false }));
        dispatch(
          setUser({
            is_superuser: false,
            username: "",
          })
        );
      }
    }, [dispatch]);

    return <WrappedComponent {...props} />;
  };

  return HOC;
};

export default withAuth;
