import { DetailedHTMLProps, HTMLAttributes, ReactNode } from "react";

export interface BlockTypeToursProps extends DetailedHTMLProps<HTMLAttributes<HTMLDivElement>, HTMLDivElement> {
    block_style?: 'viewed_block';
    children: ReactNode;   
}