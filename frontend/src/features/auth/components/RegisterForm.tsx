import { MouseEvent, useState, FC, Fragment } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { faCoins } from '@fortawesome/free-solid-svg-icons';
import { useDispatch } from 'react-redux';
import './css/RegisterForm.css';

import { Collapser } from '@/components/Animation';
import { Button, IconButton } from '@/components/Buttons';
import { Container, Flexer, Item } from '@/components/Containers';
import { Text } from '@/components/Elements';
import { Input } from '@/components/Form';
import { Icon } from '@/components/Media';
import { handleDataChange } from '@/utils';

import { advancedRegisterFields, registerFields, registerInitialData } from '../api/registerConst';
import { useRegister } from '../api/useRegister';

// Form Validation

const RegisterForm: FC = ({}) => {
  const dispatch = useDispatch();
  const navigate = useNavigate();

  const [error, setError] = useState<any>();
  const [formData, setFormData] = useState(registerInitialData);
  const [isAdvanced, setIsAdvanced] = useState(false);

  const handleOpen = (event: MouseEvent) => {
    event?.preventDefault();
    setIsAdvanced(!isAdvanced);
  };

  const submitLogic = async (event: any) => {
    event?.preventDefault();
    useRegister(formData, dispatch, navigate, setError);
  };

  return (
    <Fragment>
      <Icon icon={faCoins} color="primary" size="2rem" style={{ margin: '8px 8px 16px 8px' }} />
      <Text t="h2" a="c" className="register-heading">
        Register
      </Text>
      <Container style={{ marginTop: 8 }}>
        {registerFields.map((field: { id: string; label: string; type?: string }) => (
          <Item
            xs={field.id === 'firstName' || field.id === 'lastName' ? 6 : 12}
            style={{
              paddingRight: field.id === 'firstName' ? 3 : 0,
              paddingLeft: field.id === 'lastName' ? 3 : 0,
            }}
          >
            <Input
              id={field.id}
              name={field.id}
              type={field.type || 'text'}
              helpText={field.label}
              value={formData[field.id]}
              onChange={(e) => handleDataChange(e, setFormData, formData)}
              style={{
                marginTop: 8,
              }}
              inputStyle={{ marginTop: 2 }}
            />
          </Item>
        ))}
      </Container>
      <Flexer fd="column" j="c" mt={16}>
        <Button type="submit" size="sm" onClick={submitLogic}>
          Submit
        </Button>
        <Flexer j="fs" mt={8}>
          <Link to="/login" className="link-text">
            <Text>Already have an account? Login</Text>
          </Link>
        </Flexer>
      </Flexer>
      <Flexer j="je" mt={4}>
        <Text w="90%" a="r" mr={8}>
          Advanced Registration
        </Text>
        <IconButton
          material={isAdvanced ? 'expand_less' : 'expand_more'}
          size="t"
          fontSize="0.9rem"
          onClick={(e: MouseEvent<HTMLButtonElement>) => handleOpen(e)}
          iconStyle={{ marginTop: 1 }}
        />
      </Flexer>
      <Collapser isOpen={isAdvanced}>
        <Container>
          {advancedRegisterFields.map(
            (field: { id: string; label: string; type?: string; grid?: number }) => (
              <Item
                xs={field.grid ? field.grid : 6}
                key={field.id}
                style={{
                  paddingRight: field.id === 'city' || field.id === 'zipcode' ? 3 : 0,
                  paddingLeft: field.id === 'state' || field.id === 'country' ? 3 : 0,
                }}
              >
                <Input
                  id={field.id}
                  name={field.id}
                  type={field.type || 'text'}
                  helpText={field.label}
                  value={formData[field.id]}
                  onChange={(e) => handleDataChange(e, setFormData, formData)}
                  style={{
                    marginTop: 8,
                  }}
                  inputStyle={{ marginTop: 2 }}
                />
              </Item>
            )
          )}
        </Container>
      </Collapser>
    </Fragment>
  );
};

export default RegisterForm;
