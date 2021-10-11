import { DetailedHTMLProps, HTMLAttributes, ReactNode } from "react";

export interface BlockBreadCrumbsProps extends DetailedHTMLProps<HTMLAttributes<HTMLDivElement>, HTMLDivElement> {
    block_style?: 'viewed_block';
    margin?: 'margin_first' | 'margin_second';
    children: ReactNode;   
}