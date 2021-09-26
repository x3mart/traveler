import { DetailedHTMLProps, HTMLAttributes, ReactNode } from "react";

export interface CardCollectionProps extends DetailedHTMLProps<HTMLAttributes<HTMLDivElement>, HTMLDivElement> {
    block_style?: 'card_collection';
    children: ReactNode;   
}