import { DetailedHTMLProps, HTMLAttributes, ReactNode } from "react";

export interface SectionBlockProps extends DetailedHTMLProps<HTMLAttributes<HTMLDivElement>, HTMLDivElement> {
    block_style?: 'section_block';
    children: ReactNode;
}