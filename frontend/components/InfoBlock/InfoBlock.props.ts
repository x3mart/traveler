import { DetailedHTMLProps, HTMLAttributes, ReactNode } from "react";

export interface InfoBlockProps extends DetailedHTMLProps<HTMLAttributes<HTMLDivElement>, HTMLDivElement> {
    border_color?: 'orange_left_border' | 'blue_left_border' | 'white_left_border';
    children: ReactNode;
    
}