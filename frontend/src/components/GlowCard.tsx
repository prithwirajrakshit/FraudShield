"use client";

import React, { useRef } from "react";

interface GlowCardProps extends React.HTMLAttributes<HTMLDivElement> {
  children: React.ReactNode;
  className?: string;
}

export function GlowCard({ children, className = "", ...props }: GlowCardProps) {
  const cardRef = useRef<HTMLDivElement>(null);

  const handleMouseMove = (e: React.MouseEvent<HTMLDivElement>) => {
    const el = cardRef.current;
    if (!el) return;
    const rect = el.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    el.style.setProperty("--mouse-x", `${x}px`);
    el.style.setProperty("--mouse-y", `${y}px`);
  };

  const handleMouseLeave = () => {
    const el = cardRef.current;
    if (!el) return;
    el.style.setProperty("--mouse-x", "-999px");
    el.style.setProperty("--mouse-y", "-999px");
  };

  return (
    <div
      ref={cardRef}
      onMouseMove={handleMouseMove}
      onMouseLeave={handleMouseLeave}
      className={`glow-card ${className}`}
      {...props}
    >
      <div className="glow-card-spotlight" aria-hidden="true" />
      {children}
    </div>
  );
}

