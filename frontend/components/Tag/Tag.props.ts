import { DetailedHTMLProps, HTMLAttributes, ReactNode } from "react";

export interface TagProps extends DetailedHTMLProps<HTMLAttributes<HTMLDivElement>, HTMLDivElement> {
    size?: 's' | 'm' | 'b' | 'l' | 't' | 'feedback';
    children: ReactNode;
    href?: string;
}