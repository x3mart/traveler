import { DetailedHTMLProps, HTMLAttributes, ReactNode } from "react";

export interface CardCollectionProps extends DetailedHTMLProps<HTMLAttributes<HTMLDivElement>, HTMLDivElement> {
    name_block?: 'viewed' | 'popular' | 'personal' | 'new' | 'type' | 'rating' | 'experts' | 'sales' | 'feedback' | 'tour-page' | 'about_expert';
    block_style?: 'card_collection';
    children: ReactNode;   
}