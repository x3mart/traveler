import { DetailedHTMLProps, HTMLAttributes, ReactNode } from "react";

export interface CardTypeTourProps extends DetailedHTMLProps<HTMLAttributes<HTMLDivElement>, HTMLDivElement> {
    block_style?: 'card_tour';
    // children: ReactNode;   
}