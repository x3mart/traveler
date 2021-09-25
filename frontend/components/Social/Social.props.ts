import { DetailedHTMLProps, HTMLAttributes, ReactNode } from "react";

export interface SocialProps extends DetailedHTMLProps<HTMLAttributes<HTMLDivElement>, HTMLDivElement> {
    size?: 'social_wide';
    children: ReactNode;
    href?: string;
}