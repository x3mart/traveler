import { DetailedHTMLProps, HTMLAttributes, ReactNode } from "react";

export interface TypeTourPageProps extends DetailedHTMLProps<HTMLAttributes<HTMLDivElement>, HTMLDivElement> {
    // block_style?: 'presentation_block' | 'presentation_block_another';
    children: ReactNode;   
}