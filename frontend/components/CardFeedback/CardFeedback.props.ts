import { DetailedHTMLProps, HTMLAttributes, ReactNode } from "react";

export interface CardFeedbackProps extends DetailedHTMLProps<HTMLAttributes<HTMLDivElement>, HTMLDivElement> {
    block_style?: 'card_tour';
    // children: ReactNode;   
}