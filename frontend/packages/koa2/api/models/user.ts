import {
  DataTypes,
  InferAttributes,
  InferCreationAttributes,
  NonAttribute,
  HasOneCreateAssociationMixin,
  HasOneGetAssociationMixin,
  HasOneSetAssociationMixin,
} from 'sequelize';
import bcrypt from 'bcrypt';

import { Field } from '../core/decorators/models';
import { logger, sequelize } from '../settings';
import { SyModel } from '../core/SyModel';

import { Profile } from './profile';
import { faker } from '@faker-js/faker';

/**
 * Enumeration of user roles.
 */
export enum UserRoleEnum {
  SUPER = 'super',
  ADMIN = 'admin',
  USER = 'user',
}

/**
 * Enumeration of theme options for users.
 */
export enum ThemeEnum {
  LIGHT = 'light',
  DARK = 'dark',
}

export class User extends SyModel<
  InferAttributes<User, { omit: 'profile' }>,
  InferCreationAttributes<User, { omit: 'profile' }>
> {
  @Field({
    type: DataTypes.STRING(40),
    allowNull: false,
    verbose: 'Username',
  })
  declare username: string;

  @Field({
    type: DataTypes.STRING(500),
    allowNull: false,
    verbose: 'Password',
  })
  declare password: string;

  @Field({
    type: DataTypes.STRING(500),
    verbose: 'Salt',
  })
  declare salt?: string;

  @Field({
    type: DataTypes.STRING(500),
    verbose: 'Refresh Token',
  })
  declare refreshToken?: string;

  @Field({
    type: DataTypes.ENUM(...Object.values(UserRoleEnum)),
    allowNull: false,
    verbose: 'User Role',
    defaultValue: UserRoleEnum.USER,
  })
  declare role?: UserRoleEnum;

  @Field({
    type: DataTypes.ENUM(...Object.values(ThemeEnum)),
    allowNull: false,
    verbose: 'User Theme',
    defaultValue: ThemeEnum.DARK,
  })
  declare theme?: ThemeEnum;

  declare getProfile: HasOneGetAssociationMixin<Profile>;
  declare createProfile: HasOneCreateAssociationMixin<Profile>;
  declare setProfile: HasOneSetAssociationMixin<Profile, 'userId'>;
  declare profile?: NonAttribute<Profile>;

  /**
   * Creates a blank profile for the user.
   * @param user The user instance.
   */
  public async createBlankProfile(user: User) {
    const fields = Profile.getKeys();
    const emptyProfile: { [key: string]: string } = {};

    for (const field of fields) {
      emptyProfile[field] = '';
    }

    await user.createProfile(emptyProfile);
  }

  /**
   * Hashes the given password using bcrypt.
   * @param password The password to hash.
   * @returns An object containing the hashed password and salt.
   */
  protected static async hashPassword(password: string) {
    const saltRounds = 10;
    const salt = await bcrypt.genSalt(saltRounds);
    const hashedPassword = await bcrypt.hash(password, salt);
    return {
      password: hashedPassword,
      salt,
    };
  }

  /**
   * Hooks to be executed before and after creating user instances.
   */
  public static hooks = {
    beforeCreate: async (instance: User) => {
      const { password, salt } = await this.hashPassword(instance.password);
      instance.password = password;
      instance.salt = salt;
    },
    beforeBulkCreate: async (instances: User[]) => {
      for (const instance of instances) {
        const { password, salt } = await this.hashPassword(instance.password);
        instance.password = password;
        instance.salt = salt;
      }
    },
    afterCreate: async (user: User) => {
      user.createBlankProfile(user);
    },
  };

  /**
   * Seeds the User model with the specified number of dummy user data.
   * @param count The number of users to seed.
   */
  static async seedUser(count: number) {
    try {
      const userData = [];

      for (let i = 0; i < count; i++) {
        const username = faker.internet.userName();
        const password = faker.internet.password();

        userData.push({ username, password });
      }

      await User.bulkCreate(userData);

      logger.info('User seeding completed successfully.');
    } catch (error) {
      logger.error('User seeding failed:', error);
    }
  }
}

User.init(
  {
    ...SyModel.metaFields,
    ...User.fields,
  },
  {
    hooks: User.hooks,
    tableName: 'users',
    sequelize,
  }
);

Profile.belongsTo(User, { targetKey: 'id' });
User.hasOne(Profile, { sourceKey: 'id' });

//

export async function doStuffWithUser() {
  const newUser = await User.create({
    username: 'Johnny',
    password: 'John',
  });
  logger.info(newUser.id, newUser.username, newUser.password);
}

// User.seedUser(10);
// logger.info(User.metadata);
// logger.info(User.fields);
// logger.info(User.getKeys());
