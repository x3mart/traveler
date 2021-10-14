import { DetailedHTMLProps, HTMLAttributes, ReactNode } from "react";

export interface BlockTeamProps extends DetailedHTMLProps<HTMLAttributes<HTMLDivElement>, HTMLDivElement> {
    block_style?: 'viewed_block';
    children: ReactNode;   
}