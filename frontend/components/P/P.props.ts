import { DetailedHTMLProps, HTMLAttributes, ReactNode } from "react";

export interface PProps extends DetailedHTMLProps<HTMLAttributes<HTMLParagraphElement>, HTMLParagraphElement> {
    color?: 'p_footer';
    link?: 'p_footer_link' | 'p_footer_link_col_2' | 'p_footer_letter_spacing' | 'p_footer_letter_spacing_margin_top';
    children: ReactNode;
    href?: string;
}