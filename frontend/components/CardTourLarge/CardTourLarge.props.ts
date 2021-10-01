import { DetailedHTMLProps, HTMLAttributes, ReactNode } from "react";

export interface CardTourLargeProps extends DetailedHTMLProps<HTMLAttributes<HTMLDivElement>, HTMLDivElement> {
    block_style?: 'card_tour';
    // children: ReactNode;   
}