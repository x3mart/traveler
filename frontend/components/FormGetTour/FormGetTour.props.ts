import { DetailedHTMLProps, HTMLAttributes, ReactNode } from "react";

export interface FormGetTourProps extends DetailedHTMLProps<HTMLAttributes<HTMLDivElement>, HTMLDivElement> {
    form_style?: 'first_form_get_tour';
    children: ReactNode;
}