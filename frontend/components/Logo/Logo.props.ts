import { DetailedHTMLProps, HTMLAttributes, ReactNode } from "react";

export interface LogoProps extends DetailedHTMLProps<HTMLAttributes<HTMLDivElement>, HTMLDivElement> {
    // color?: 'logo_header' | 'logo_footer';
    children: ReactNode;
    href?: string;
}