import test from 'node:test';
import assert from 'node:assert/strict';
import {quoteSchema,safeImage,internationalPhone} from '../src/lib/validation';
const valid={name:'Test Buyer',company:'QA Trading',email:'buyer@example.com',phone:'+971501234567',location:'Dubai',notes:'Test only',website:'',items:[{categoryId:'soft-drinks',requirement:'Requested brand, 330 ml',quantity:'10',unit:'Cases'}]};
test('accepts multi-item category and product requests',()=>{const result=quoteSchema.parse({...valid,items:[...valid.items,{...valid.items[0],productId:'genuine-product'}]});assert.equal(result.items.length,2);assert.equal(result.items[0].quantity,10);});
test('rejects empty baskets, negative quantities and spam honeypots',()=>{for(const bad of [{...valid,items:[]},{...valid,items:[{...valid.items[0],quantity:-1}]},{...valid,website:'spam'}])assert.equal(quoteSchema.safeParse(bad).success,false);});
test('rejects oversized requests and invalid contact information',()=>{assert.equal(quoteSchema.safeParse({...valid,items:Array(21).fill(valid.items[0])}).success,false);assert.equal(quoteSchema.safeParse({...valid,email:'bad',notes:'a'.repeat(5001)}).success,false);});
test('unverified original number cannot become a clickable phone number',()=>{assert.equal(internationalPhone.safeParse('9713749234').success,false);assert.equal(internationalPhone.safeParse('+971501234567').success,true);});
test('media validation prevents external hosts, executable URLs and traversal',()=>{for(const bad of ['javascript:alert(1)','https://evil.test/photo.jpg','/media/../../secret','/media/test.svg'])assert.equal(safeImage.safeParse(bad).success,false);assert.equal(safeImage.safeParse('/media/1234abcd-1234.webp').success,true);});
