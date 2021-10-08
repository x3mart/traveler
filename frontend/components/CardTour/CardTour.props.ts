import { DetailedHTMLProps, HTMLAttributes, ReactNode } from "react";

export interface CardTourProps extends DetailedHTMLProps<HTMLAttributes<HTMLDivElement>, HTMLDivElement> {
    block_style?: 'card_tour' | 'card_tour_border';
    block_width?: 'block_width_travel_page' | 'display_none';
    // children: ReactNode;   
}