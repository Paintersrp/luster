import React, { useState } from "react";
import "../styles.css";
import { faChevronDown } from "@fortawesome/free-solid-svg-icons";

import BaseIconButton from "../../BaseIconButton/BaseIconButton";
import Collapser from "../../Collapser/Collapser";
import Divider from "../../Divider/Divider";
import Flexer from "../../Flexer/Flexer";
import Text from "../../Text/Text";

import { shadowSwitch } from "../../../../utils/styleSwitches/styleSwitches";

function Section({
  header,
  children,
  maxWidth,
  boxShadow = 0,
  mb: marginBottom = 3,
  mt: marginTop = 3,
  pad: padding = 3,
  pl: paddingLeft = 0,
  pr: paddingRight = 0,
  pt: paddingTop = 0,
  pb: paddingBottom = 0,
  br: borderRadius = 1,
  b: background = "#F5F5F5",
  j: justifyChildren = "flex-start",
  a: alignChildren = "flex-start",
  fd = "column",
  collapse = false,
  divider = false,
  gutter = false,
  headerAlign = "center",
  headerVar = "h3",
  centerAlignIconPosition = "right",
}) {
  const [open, setOpen] = useState(true);

  return (
    <Flexer
      j="c"
      pl={paddingLeft * 8}
      style={{
        height: "100%",
        margin: 0,
        paddingRight: paddingRight * 8,
        paddingTop: paddingTop * 8,
        paddingBottom: paddingBottom * 8,
        marginBottom: gutter ? 16 : 0,
        background: background,
      }}
    >
      <div
        style={{
          height: "100%",
          maxWidth: maxWidth,
          padding: padding * 8,
          boxShadow: shadowSwitch(boxShadow),
          borderRadius: borderRadius * 8,
          background: background,
          marginBottom: marginBottom * 8,
          marginTop: marginTop * 8,
          width: "100%",
        }}
      >
        <Flexer j="c">
          <Flexer
            a="c"
            style={{
              textAlign: headerAlign,
              order:
                headerAlign === "right" && collapse
                  ? 1
                  : headerAlign === "center" && collapse
                  ? centerAlignIconPosition === "right"
                    ? 0
                    : 1
                  : 1,
              marginLeft:
                headerAlign === "center" && collapse
                  ? centerAlignIconPosition === "right"
                    ? 26
                    : 0
                  : 0,
              marginRight:
                headerAlign === "center" && collapse
                  ? centerAlignIconPosition === "left"
                    ? 26
                    : 0
                  : 0,
            }}
          >
            {header && (
              <Text t={headerVar} className="header" a={headerAlign}>
                {header}
              </Text>
            )}
          </Flexer>

          {collapse && (
            <Flexer
              j="c"
              a="c"
              w={26}
              style={{
                order:
                  headerAlign === "right" && collapse
                    ? 0
                    : headerAlign === "center" && collapse
                    ? centerAlignIconPosition === "right"
                      ? 1
                      : 0
                    : 1,
              }}
            >
              <BaseIconButton
                className={`expandButton ${open ? "rotate" : ""}`}
                size="tiny"
                onClick={() => setOpen(!open)}
                icon={faChevronDown}
                fontSize="0.9rem"
              />
            </Flexer>
          )}
        </Flexer>
        {divider && <Divider mt={2} mb={8} color="rgba(0, 0, 0, 0.38)" />}

        <Collapser isOpen={open}>
          <Flexer j={justifyChildren} a={alignChildren} fd={fd}>
            {children}
          </Flexer>
        </Collapser>
      </div>
    </Flexer>
  );
}

export default Section;
