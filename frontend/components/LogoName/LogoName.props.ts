import { DetailedHTMLProps, HTMLAttributes, ReactNode } from "react";

export interface LogoNameProps extends DetailedHTMLProps<HTMLAttributes<HTMLDivElement>, HTMLDivElement> {
    color?: 'logo_header' | 'logo_footer';
    children: ReactNode;
    href?: string;
}