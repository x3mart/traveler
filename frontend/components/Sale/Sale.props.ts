import { DetailedHTMLProps, HTMLAttributes, ReactNode } from "react";

export interface SaleProps extends DetailedHTMLProps<HTMLAttributes<HTMLDivElement>, HTMLDivElement> {
    children: ReactNode;
    
}