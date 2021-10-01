import { DetailedHTMLProps, HTMLAttributes, ReactNode } from "react";

export interface HtagProps extends DetailedHTMLProps<HTMLAttributes<HTMLDivElement>, HTMLDivElement> {
    tag: 'h1' | 'h2' | 'h3' | 'h4';
    // text_align?: 'center' | 'left' | 'right';
    children: ReactNode;
}