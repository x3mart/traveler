import { DetailedHTMLProps, HTMLAttributes, ReactNode } from "react";

export interface CardCountryTourProps extends DetailedHTMLProps<HTMLAttributes<HTMLDivElement>, HTMLDivElement> {
    block_style?: 'card_tour';
    // children: ReactNode;   
}