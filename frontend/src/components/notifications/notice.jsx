import React from "react";
import './notice.css'

export default function NoticeBody({ msg }) {
  return <div className="noticeText">
      <p>{msg}</p>
    </div>;
}