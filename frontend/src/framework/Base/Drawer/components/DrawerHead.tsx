import React, { ReactNode } from "react";
import { palettes } from "../../../../theme";

import Flexer, { JustificationValue } from "../../../Containers/Flexer/Flexer";
import Divider from "../../Divider/Divider";

interface DrawerHeadProps {
  j?: JustificationValue;
  a?: JustificationValue;
  title?: string;
  icon?: ReactNode;
  children?: ReactNode;
  color?: keyof typeof palettes;
}

const DrawerHead: React.FC<DrawerHeadProps> = ({
  j: justifyContent = "center",
  a: alignItems = "center",
  title,
  icon,
  children,
  color = "primary",
}) => {
  return (
    <>
      <Flexer j={justifyContent} a={alignItems} style={{ height: 63 }}>
        <Flexer j="c">
          {icon && (
            <span
              style={{
                position: "absolute",
                display: "flex",
                left: 0,
                marginLeft: 24,
              }}
            >
              {icon && icon}
            </span>
          )}
          {title && <h3>{title}</h3>}
        </Flexer>
        {children}
      </Flexer>
      <Divider color={palettes[color].hover} thickness={1} />
    </>
  );
};

export default DrawerHead;
