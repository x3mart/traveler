import { DetailedHTMLProps, HTMLAttributes, ReactNode } from "react";

export interface BlockViewedProps extends DetailedHTMLProps<HTMLAttributes<HTMLDivElement>, HTMLDivElement> {
    block_style?: 'viewed_block' | 'white';
    children: ReactNode;   
}