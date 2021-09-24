import { ButtonHTMLAttributes, DetailedHTMLProps, ReactNode } from "react";

export interface ButtonProps extends DetailedHTMLProps<ButtonHTMLAttributes<HTMLButtonElement>, HTMLButtonElement> {
    children: ReactNode;
    appearance: 'primary' | 'ghost' | 'header_button' | 'header_button_travel' | 'header_button_support' |
                'header_button_country' | 'header_button_currency' | 'header_button_liked' | 'header_button_enter';
    arrow?: 'right' | 'down' | 'none';
    traveler_suitcase?: 'true' | 'none';
}