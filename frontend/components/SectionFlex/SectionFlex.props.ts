import { DetailedHTMLProps, HTMLAttributes, ReactNode } from "react";

export interface SectionFlexProps extends DetailedHTMLProps<HTMLAttributes<HTMLDivElement>, HTMLDivElement> {
    block_style?: 'section_flex';
    children: ReactNode;
}