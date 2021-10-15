import styles from './CardTour.module.css';
import { CardTourProps } from './CardTour.props';
import cn from 'classnames';
import { Tag, Htag } from '../../components/';
import StarIcon from '/public/Star.svg';
import LikeIcon from '/public/Like.svg';
import Link from 'next/link';
    


export const CardTour = ({ block_style, block_width, children, className, ...props }: CardTourProps): JSX.Element => {    
    return (
        <div
            className={ cn(styles.card_tour, className, {
                [styles.card_tour]: block_style == 'card_tour',
                [styles.card_tour_border]: block_style == 'card_tour_border',
                [styles.block_width_travel_page]: block_width == 'block_width_travel_page',
                [styles.display_none]: block_width == 'display_none',
            })}
            {...props}
            
        >    
                  
            {children}
            <Tag size='b'>
                <Link href='/tour/detail-tour/'>
                    <div className={styles.card_tour_image}>
                        <LikeIcon />                    
                    </div>
                </Link>
                <div className={styles.card_tour_content}>
                    <div className={styles.card_tour_content_place_info}>
                        <Htag tag='h4'>Вьетнам</Htag>
                        <Link href='/tour/detail-tour/'>
                            <Htag className={styles.link_pointer} tag='h3'>Неизведанные места и тропы</Htag>
                        </Link>
                    </div>
                    <div className={styles.card_tour_content_guide_info}>
                        <div className={styles.card_tour_content_guide_info_name}>
                        <Link href='/expert/'>
                            <div className={styles.card_tour_content_guide_info_name_avatar}>

                            </div>
                        </Link>
                            <div className={styles.card_tour_content_guide_info_name_raiting}>                                
                                <Htag tag='h4'><Link href='/expert/'>Мария</Link></Htag>                                
                                <Htag tag='h4'>
                                    <StarIcon />
                                    <span className={styles.raiting_star}>4.9</span>
                                    (132)  
                                </Htag>
                            </div>
                        </div>
                        <div className={styles.card_tour_content_guide_info_cost}>
                            <Htag tag='h4'>7 дн. (21 - 28 мар)</Htag> 
                            <Htag tag='h3'>от 80.000 <span>{'\u20bd'}</span></Htag>
                        </div>
                    </div>
                </div>
            </Tag>     
             
        </div>
    );
};