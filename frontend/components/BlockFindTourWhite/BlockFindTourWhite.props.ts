import { DetailedHTMLProps, HTMLAttributes, ReactNode } from "react";

export interface BlockFindTourWhiteProps extends DetailedHTMLProps<HTMLAttributes<HTMLDivElement>, HTMLDivElement> {
    block_style?: 'viewed_block';
    children: ReactNode;   
}