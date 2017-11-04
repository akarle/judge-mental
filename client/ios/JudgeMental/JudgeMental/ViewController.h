//
//  ViewController.h
//  JudgeMental
//
//  Created by Makenzie Schwartz on 11/4/17.
//  Copyright © 2017 Makenzie Schwartz. All rights reserved.
//

#import <UIKit/UIKit.h>
@import UIKit;
@import AVFoundation;

@interface ViewController : UIViewController {
    IBOutlet UILabel *label;
    bool cameraAvail;
}

@property (retain, nonatomic) IBOutlet UILabel *label;


@end

