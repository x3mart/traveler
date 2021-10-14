import { DetailedHTMLProps, HTMLAttributes, ReactNode } from "react";

export interface TagProps extends DetailedHTMLProps<HTMLAttributes<HTMLDivElement>, HTMLDivElement> {
    size?: 's' | 'm' | 'b' | 'l' | 't' | 'feedback' | 'about_expert';
    children: ReactNode;
    href?: string;
}