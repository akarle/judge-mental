//
//  ViewController.m
//  JudgeMental
//
//  Created by Makenzie Schwartz on 11/4/17.
//  Copyright © 2017 Makenzie Schwartz. All rights reserved.
//

#import "ViewController.h"

@interface ViewController () <UINavigationControllerDelegate, UIImagePickerControllerDelegate>

@property (nonatomic) UIImagePickerController *imagePickerController;
@property (nonatomic) IBOutlet UIButton *judgeButton;
@property (nonatomic) IBOutlet UILabel *askLabel;
@property (nonatomic) IBOutlet UIImageView *stars;
@property (nonatomic) IBOutlet UIImageView *starCover;
@property (nonatomic) IBOutlet UILabel *scoreLabel;
@property (nonatomic) IBOutlet UIButton *againButton;
@property (nonatomic) IBOutlet UILabel *againLabel;

@end

@implementation ViewController

- (void)viewDidLoad {
    [super viewDidLoad];
    // Do any additional setup after loading the view, typically from a nib.
    if (![UIImagePickerController isSourceTypeAvailable:UIImagePickerControllerSourceTypeCamera]) {
        cameraAvail = false;
    } else {
        cameraAvail = true;
    }
    initialMaskPos = _starCover.center.x;
}


- (void)didReceiveMemoryWarning {
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}

- (IBAction)buttonPressed {
    if (cameraAvail) {
        _imagePickerController = [[UIImagePickerController alloc] init];
        _imagePickerController.sourceType = UIImagePickerControllerSourceTypeCamera;
        _imagePickerController.delegate = self;
        [self presentViewController:_imagePickerController animated:YES completion:nil];
    }
}

- (IBAction)retryButtonPressed {
    [_scoreLabel setHidden:YES];
    [_againButton setHidden:YES];
    [_againButton setEnabled:NO];
    [_againLabel setHidden:YES];
    [_stars setHidden:YES];
    [_starCover setHidden:YES];
    [_starCover setCenter:CGPointMake(initialMaskPos, _starCover.center.y)];
    [_judgeButton setHidden:NO];
    [_judgeButton setEnabled:YES];
    [_askLabel setHidden:NO];
}

- (void)imagePickerController:(UIImagePickerController *)picker didFinishPickingMediaWithInfo:(NSDictionary<NSString *,id> *)info {
    UIImage *image = [info objectForKey:UIImagePickerControllerOriginalImage];
    
    // Post to server
    NSMutableDictionary *_params = [[NSMutableDictionary alloc] init];
    NSString *BoundaryConstant = [NSString stringWithString:@"----------V2ymHFg03ehbqgZCaKO6jy"];
    NSString *FileParamConstant = [NSString stringWithString:@"file"];
    
    NSURL *requestURL = [NSURL URLWithString:@"http://judge-mental.tech:8080/upload"];
    
    NSMutableURLRequest *request = [[NSMutableURLRequest alloc] init];
    [request setCachePolicy:NSURLRequestReloadIgnoringCacheData];
    [request setHTTPShouldHandleCookies:NO];
    [request setTimeoutInterval:30];
    [request setHTTPMethod:@"POST"];
    
    NSString *contentType = [NSString stringWithFormat:@"multipart/form-data; boundary=%@", BoundaryConstant];
    [request setValue:contentType forHTTPHeaderField:@"Content-Type"];
    
    NSMutableData *body = [NSMutableData data];
    
    NSData *imageData = UIImageJPEGRepresentation(image, 1.0);
    if (imageData) {
        [body appendData:[[NSString stringWithFormat:@"--%@\r\n", BoundaryConstant] dataUsingEncoding:NSUTF8StringEncoding]];
        [body appendData:[[NSString stringWithFormat:@"Content-Disposition: form-data; name=\"%@\"; filename=\"image.jpg\"\r\n", FileParamConstant] dataUsingEncoding:NSUTF8StringEncoding]];
        [body appendData:[[NSString stringWithString:@"Content-Type: image/jpeg\r\n\r\n"] dataUsingEncoding:NSUTF8StringEncoding]];
        [body appendData:imageData];
        [body appendData:[[NSString stringWithFormat:@"\r\n"] dataUsingEncoding:NSUTF8StringEncoding]];
    }
    
    [body appendData:[[NSString stringWithFormat:@"--%@--\r\n", BoundaryConstant] dataUsingEncoding:NSUTF8StringEncoding]];
    
    [request setHTTPBody:body];
    
    NSString *postLength = [NSString stringWithFormat:@"%d", [body length]];
    [request setValue:postLength forHTTPHeaderField:@"Content-Length"];
    
    [request setURL:requestURL];
    
    NSURLSessionConfiguration *defaultConfigObject = [NSURLSessionConfiguration defaultSessionConfiguration];
    NSURLSession *defaultSession = [NSURLSession sessionWithConfiguration:defaultConfigObject delegate:nil delegateQueue:[NSOperationQueue mainQueue]];
    [_judgeButton setHidden:YES];
    [_judgeButton setEnabled:NO];
    [_askLabel setHidden:YES];
    DGActivityIndicatorView *activityIndicatorView = [[DGActivityIndicatorView alloc] initWithType:DGActivityIndicatorAnimationTypeNineDots tintColor:[UIColor whiteColor] size:150.0f];
    CGRect screenRect = [[UIScreen mainScreen] bounds];
    CGFloat screenWidth = screenRect.size.width;
    CGFloat screenHeight = screenRect.size.height;
    activityIndicatorView.frame = CGRectMake(screenWidth / 2.0f - 75.0f, screenHeight / 2.0f - 50.0f, 150.0f, 150.0f);
    [self.view addSubview:activityIndicatorView];
    [activityIndicatorView startAnimating];
    NSURLSessionDataTask *dataTask = [defaultSession dataTaskWithRequest:request completionHandler:^(NSData *data, NSURLResponse *response, NSError *error) {
        if (error == nil) {
            NSString *text = [[NSString alloc] initWithData:data encoding:NSUTF8StringEncoding];
            NSLog(@"Data = %@",text);
            float value = text.floatValue;
            if (value != -99) {
                float mask = (5.0f - value) / 5.0f;
                [_starCover setCenter:CGPointMake(_starCover.center.x - _starCover.frame.size.width * mask, _starCover.center.y)];
                [_stars setHidden:NO];
                [_starCover setHidden:NO];
                [_againLabel setHidden:NO];
                [_againButton setHidden:NO];
                [_againButton setEnabled:YES];
                _scoreLabel.text = [NSString stringWithFormat:@"JudgeMental says: %.02f", value];
                [_scoreLabel setHidden:NO];
            } else {
                [_againLabel setHidden:NO];
                [_againButton setHidden:NO];
                [_againButton setEnabled:YES];
                _scoreLabel.text = [NSString stringWithFormat:@"Error extracting text..."];
                [_scoreLabel setHidden:NO];
            }
        } else {
            NSLog(@"Error = %@",error);
            [_againLabel setHidden:NO];
            [_againButton setHidden:NO];
            [_againButton setEnabled:YES];
            _scoreLabel.text = [NSString stringWithFormat:@"Unknown error!"];
            [_scoreLabel setHidden:NO];
        }
        [activityIndicatorView stopAnimating];
        [activityIndicatorView removeFromSuperview];
    }];
    
    
    [dataTask resume];
    
    [self dismissViewControllerAnimated:YES completion:nil];
}

@end
