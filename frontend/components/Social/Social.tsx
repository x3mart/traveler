import styles from './Social.module.css';
import { SocialProps } from './Social.props';
import cn from 'classnames';
import FacebookIcon from '/public/14.svg';
import TwitterIcon from '/public/15.svg';
import VKIcon from '/public/16.svg';
import InstagramIcon from '/public/17.svg';
import YoutubeIcon from '/public/18.svg';


export const Social = ({ size, children, href, className, ...props }: SocialProps): JSX.Element => {    
    return (
        <div
            className={ cn(styles.social, className, {                
                [styles.social_wide]: size == 'social_wide',
            })}
            {...props}
        >{
            href
                ? <a href={href}>{children}</a>
                : <>
                    {children}
                    <FacebookIcon />
                    <TwitterIcon />
                    <VKIcon />
                    <InstagramIcon />
                    <YoutubeIcon />
                  </>
        }   
            
        </div>
    );
};