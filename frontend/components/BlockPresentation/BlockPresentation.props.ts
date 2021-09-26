import { DetailedHTMLProps, HTMLAttributes, ReactNode } from "react";

export interface BlockPresentationProps extends DetailedHTMLProps<HTMLAttributes<HTMLDivElement>, HTMLDivElement> {
    block_style?: 'presentation_block';
    children: ReactNode;   
}